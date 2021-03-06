use strict;
use warnings;

use Test::More;
use File::Slurp;
use JSON;
use URI;

my $test_data = decode_json( read_file('t/test_data/url_creation.json') );
my @tests     = @{ $test_data->{tests} };

plan tests => 2 + 2 * @tests;

use_ok 'WWW::Privatar';

ok my $privatar = WWW::Privatar->new( $test_data->{config} );

foreach my $test (@tests) {
    my %args = %{ $test->{args} };

    my $url = $privatar->url( \%args );
    ok( URI::eq( $url, $test->{urls}{http} ), $test->{msg} )
      || diag "got:      '$url'\nexpected: '$test->{urls}{http}'";

    my $secure_url = $privatar->url( { %args, secure => 1 } );
    ok( URI::eq( $secure_url, $test->{urls}{https} ), $test->{msg} )
      || diag "got:      '$secure_url'\nexpected: '$test->{urls}{https}'";
}

