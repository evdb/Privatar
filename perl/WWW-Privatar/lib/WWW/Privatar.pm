package WWW::Privatar;

use strict;
use warnings;

our $VERSION = '0.01';

use Digest::MD5;
use URI;
use Carp;

=head1 NAME

WWW::Privatar - generate urls for the privacy enhancing Gravatar proxy

=head1 METHODS

=head2 new

    $privatar = WWW::Privatar->new({
        site_key     => 'yoursitecode',
        shared_secret => 'xxx',
    });

Create a new privatar object. Pass in E<site_key> and E<shared_secret> to set
these for future method calls.

=cut

sub new {
    my $class = shift;
    my $args = shift || {};

    my $self = {
        http_base => 'http://www.privatar.org',
        %$args
    };

    for ( 'site_key', 'shared_secret', ) {
        croak "Required parameter '$_' missing" if !$self->{$_};
    }

    return bless $self, $class;
}

sub http_base     { $_[0]->{http_base} }
sub site_key      { $_[0]->{site_key} }
sub shared_secret { $_[0]->{shared_secret} }

=head2 url

    $uri_object = $privatar->url({
        email_md5 => '00112233445566778899aabbccddeeff',
    });

Create a url.

=cut

sub url {
    my $self = shift;
    my $args = shift || {};

    my $avatar_code = $self->generate_avatar_code($args);

    my $uri = URI->new( $self->http_base );
    $uri->path("/avatar/$avatar_code");
    $uri->query_form( $args->{query} || {} );
    return $uri;
}

=head2 generate_avatar_code

    $avatar_code = $privatar->generate_avatar_code({
        email     => 'joe@example.com',                     # either...
        email_md5 => 'f5b8fb60c6116331da07c65b96a8a1d1',    # ...or
        salt      => 'xyzxyz',                              # optional
    });

Create the privatar code for this site/email combination. Requires an E<email>
or an E<email_md5>. Optionally you can provide a E<salt> or let the code produce
one for you. The salt should be unique to the user and should not reveal
anything about them. If in doubt let the code produce one for you.

=cut

sub generate_avatar_code {
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

    # return the avatar code
    return join '-', $self->site_key, $salt, $encrypted_md5;
}

=head2 generate_salt

    $salt = $privatar->generate_salt( $email_md5 );

Generate the salt for this E<email_md5>.

The salt is something unique to each email on the site and is used to prevent
replay attacks. It also needs to be anonymous so it is created by md5ing the
E<site_key>, the E<shared_secret> and the E<email_md5> and then shortening the
result to an 8 character string.

=cut

# yeah yeah - there is no guarantee that the resulting string will be unique for
# each user but it is as good as. Let's not get carried away here. It's going to
# be vey unlikely there is a clash.

sub generate_salt {
    my $self = shift;
    my $email_md5 = shift || croak "Need an argument";

    # create the md5 hash
    my $hash = _md5( $self->shared_secret, $email_md5 );

    # convert the hash from hex to something more information dense
    return substr $hash, 0, 8;
}

=head2 xor_md5s

    $encrypted = WWW::Privatar->xor_md5s( $key_md5, $input_md5 );
    $input_md5 = WWW::Privatar->xor_md5s( $key_md5, $encrypted );

Returns a 32 character long hex sring which is the result of XORing the key and
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
