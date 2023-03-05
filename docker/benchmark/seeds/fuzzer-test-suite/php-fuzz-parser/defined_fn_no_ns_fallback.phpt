<?php

namespace Foo;

var_dump(\defined('Foo\PHP_INT_MAX'));

$const = 'Foo\PHP_INT_MAX';
var_dump(\defined($const));

?>