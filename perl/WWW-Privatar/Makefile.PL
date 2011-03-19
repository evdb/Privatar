use strict;
use warnings;

use ExtUtils::MakeMaker;

my $MM = WriteMakefile(
    NAME          => 'WWW::Privatar',
    VERSION_FROM  => "lib/WWW/Privatar.pm",
    ABSTRACT_FROM => "lib/WWW/Privatar.pm",
    AUTHOR        => 'Edmund von der Burg <evdb@cpan.org>',
    PREREQ_PM     => {
        'Carp'         => 0,
        'Digest::MD5'  => 0,
        'URI'          => 0,
        'Readonly'     => 0,
        'Math::Base36' => 0,
    },
    CONFIGURE_REQUIRES => {    #
        'ExtUtils::MakeMaker' => 0,
    },
    BUILD_REQUIRES => {
        'File::Slurp' => 0,
        'JSON'        => 0,
        'Test::More'  => 0,
    },

    LICENSE => 'perl',

    META_MERGE => {
        resources => {
            homepage   => 'http://www.privatar.org',
            bugtracker => 'https://github.com/evdb/Privatar/issues',
            repository => 'https://github.com/evdb/Privatar',
        },
    },
);
