use strict;
use warnings;

use Test::More;
use File::Slurp;
use JSON;

my $tests = decode_json( read_file('t/test_data/url_conversion.json') );

plan tests => 2 + @$tests;

use_ok 'WWW::Privatar';

ok my $privatar = WWW::Privatar->new(
    {
        site_key      => 'testsite',
        shared_secret => 'testsharedsecret',
    }
);

foreach my $test (@$tests) {
    my %args = %{ $test->{args} };

    my $url = $privatar->url( \%args );

    # my $secure_url = $privatar->url( { %args, secure => 1 } );

    is $url, $test->{urls}{http}, $test->{msg};
}

