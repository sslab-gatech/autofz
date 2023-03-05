<?php
// the trailing whitespace is intentional
$ini = <<<END
1="foo"
2="bar" ; comment
3= baz
4= "foo;bar"
5= "foo" ; bar ; baz
6= "foo;bar" ; baz
7= foo"bar ; "ok
END;

var_dump(parse_ini_string($ini, false, INI_SCANNER_RAW));
?>