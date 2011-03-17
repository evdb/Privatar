use strict;
use warnings;
use Module::Build;

my $build = Module::Build->new(
    module_name => 'WWW::Privatar',
    license     => 'perl',
    requires    => {
        'Carp'        => 0,
        'Digest::MD5' => 0,
        'URI'         => 0,
    },
    build_requires => {
        'File::Slurp' => 0,
        'JSON'        => 0,
        'Test::More'  => 0,
    },
);
$build->create_build_script;

