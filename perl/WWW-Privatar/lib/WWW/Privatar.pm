package WWW::Privatar;

use strict;
use warnings;

our $VERSION = '0.01';

use Digest::MD5;
use URI;
use URI::QueryParam;
use Carp;
use Readonly;
use Math::Base36 'encode_base36';

=head1 NAME

WWW::Privatar - generate urls for the privacy enhancing Gravatar proxy

=head1 METHODS

=head2 new

    $privatar = WWW::Privatar->new({

        # required arguments
        site_code      => 'yoursitecode',
        shared_secret => 'xxx',
        
        # optional args
        suffix => 'jpg',    # default is none
        
        # If you run your own Privatar instance
        http_base  => 'http://www.yourprivatar.com',
        https_base => 'https://secure.yourprivitar.com',
    });

Create a new privatar object. Pass in C<site_code> and C<shared_secret> to set
these for future method calls.

=cut

sub new {
    my $class = shift;
    my $args = shift || {};

    my $self = {
        http_base  => 'http://www.privatar.org',
        https_base => 'https://privatar-org.appspot.com',
        suffix     => '',
        %$args
    };

    for ( 'site_code', 'shared_secret', ) {
        croak "Required parameter '$_' missing" if !$self->{$_};
    }

    return bless $self, $class;
}

sub http_base     { $_[0]->{http_base} }
sub https_base    { $_[0]->{https_base} }
sub suffix        { $_[0]->{suffix} }
sub site_code     { $_[0]->{site_code} }
sub shared_secret { $_[0]->{shared_secret} }

=head2 url

    $uri_object = $privatar->url(
        {

            # one of these is required
            email     => 'joe@example.com',
            email_md5 => '00112233445566778899aabbccddeeff',

            # optional args
            query => { rating => 'pg' },    # added to url (values uri escaped)
            salt   => $salt_string,   # see notes below
            secure => $bool,          # true for https, false for http (default)
            suffix => 'jpg',          # added to end of url (eg 'xxx.jpg')
        }
    );

Create a url for either the C<email_md5> or C<email> (which is md5ed for you).

You may supply any of the optional arguments as needed.

NOTE - if you choose to supply a C<salt> for the user please ensure that it is
unique to the user and does not disclose any private information regarding the
user. This includes anything that might be used to compare users across sites.
Something like a user_id is probably a good fit, or let the module generate one
for you.

=cut

sub url {
    my $self = shift;
    my $args = shift || {};

    my $privatar_code = $self->generate_privatar_code($args);

    my $uri =
      URI->new( $args->{secure} ? $self->https_base : $self->http_base );

    # get the suffix and prepare it for adding to path
    my $suffix = $args->{suffix} || $self->suffix || '';
    $suffix = ".$suffix" if $suffix;

    $uri->path( "/avatar/" . $privatar_code . $suffix );

    my $query = $args->{query} || {};
    $uri->query_param( $_ => $query->{$_} ) for sort keys %$query;

    return $uri;
}

=head2 generate_privatar_code

    $privatar_code = $privatar->generate_privatar_code({
        email     => 'joe@example.com',                     # either...
        email_md5 => 'f5b8fb60c6116331da07c65b96a8a1d1',    # ...or
        salt      => 'xyzxyz',                              # optional
    });

Create the privatar code for this site/email combination. Requires an C<email>
or an C<email_md5>. Optionally you can provide a C<salt> or let the code produce
one for you. The salt should be unique to the user and should not reveal
anything about them. If in doubt let the code produce one for you.

=cut

sub generate_privatar_code {
    my $self = shift;
    my $args = shift || {};

    # get the email_md5 or croak
    my $email_md5 =
         $args->{email_md5}
      || _md5( $args->{email} )
      || croak "Required arguments 'email' or 'email_md5' missing";

    # get the salt
    my $salt = $args->{salt}
      || $self->generate_salt($email_md5);

    # create the hash to encrypt the email_md5 with
    my $one_time_pad = _md5( $salt, $self->shared_secret );

    # encrypt the email_md5
    my $encrypted_md5 = $self->xor_md5s( $email_md5, $one_time_pad );

    # get the version of the shared_secret
    my ($version) = $self->shared_secret =~ m{^(\d+)};
    $version ||= 0;

    # return the avatar code
    return join '-', $self->site_code, $version, $salt, $encrypted_md5;
}

=head2 generate_salt

    $salt = $privatar->generate_salt( $email_md5 );

Generate the salt for this C<email_md5>.

The salt is something unique to each email on the site and is used to prevent
replay attacks. It also needs to be anonymous so it is created by md5ing the
C<site_code>, the C<shared_secret> and the C<email_md5> and then shortening the
result to an 8 character base36 string.

=cut

# yeah yeah - there is no guarantee that the resulting string will be unique for
# each user but it is as good as. Let's not get carried away here. It's going to
# be vey unlikely there is a clash.

sub generate_salt {
    my $self = shift;
    my $email_md5 = shift || croak "Need an argument";

    # create the md5 hash
    my $hash = _md5( $self->shared_secret, $email_md5 );

    # create a number from the first 16 chars of hex
    use bignum;
    my $number = hex( substr $hash, 0, 16 );

    my $long_salt = lc encode_base36( $number, 8 );

    # keep it short
    return substr $long_salt, 0, 8;
}

=head2 xor_md5s

    $encrypted = WWW::Privatar->xor_md5s( $key_md5, $input_md5 );
    $input_md5 = WWW::Privatar->xor_md5s( $key_md5, $encrypted );

Returns a 32 character long hex string which is the result of XORing the key and
the input (both md5 hex digests).

Note that this is symetric - so feeding the output back in will give you the
input.

=cut

sub xor_md5s {
    my ( $class, $key, $in ) = @_;

    my @key_as_chars = split //, $key;
    my @in_as_chars  = split //, $in;
    my $out          = '';

    while ( @key_as_chars || @in_as_chars ) {
        my $result =
          hex( shift @key_as_chars || 0 ) ^ hex( shift @in_as_chars || 0 );
        $out .= sprintf '%x', $result;
    }

    return $out;
}

# utility - return false if no input or the md5_hex if there was one. If given
# several args join them with '-'.
sub _md5 {
    return unless scalar(@_) && $_[0];
    return Digest::MD5::md5_hex( join( '-', @_ ) );
}

=head1 AUTHOR

Edmund von der Burg 

=cut

1;
