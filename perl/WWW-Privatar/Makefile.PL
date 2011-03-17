use strict;
use warnings;

use inc::Module::Install;

name 'WWW::Privatar';
all_from 'lib/WWW/Privatar.pm';

requires 'Carp'             => 0;
requires 'Digest::MD5'      => 0;
requires 'URI'              => 0;

test_requires 'File::Slurp' => 0;
test_requires 'JSON'        => 0;
test_requires 'Test::More'  => 0;

WriteAll;
