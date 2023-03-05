<?php

require 'includes/foo_strlen.inc';

use function foo\strlen;

var_dump(strlen('foo bar baz'));
echo "Done\n";

?>