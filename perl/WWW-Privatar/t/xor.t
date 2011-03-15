use strict;
use warnings;

use Test::More;

use JSON;
use File::Slurp;
use WWW::Privatar;

my $tests = decode_json( read_file('t/test_data/xor_samples.json') );

plan tests => 2 * scalar @$tests;

foreach my $test (@$tests) {

    # xor to get the encrypted
    my $generated = WWW::Privatar->xor_md5s( $test->{key}, $test->{in} );
    is $generated, $test->{out}, "XOR: $test->{key} ^ $test->{in}";

    # xor again to get the input back
    my $again = WWW::Privatar->xor_md5s( $test->{key}, $generated );
    is $again, $test->{in}, "XOR again with same key returns input";
}
