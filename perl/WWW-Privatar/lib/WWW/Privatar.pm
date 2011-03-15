package WWW::Privatar;

use strict;
use warnings;

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

1;
