<?php

$a = new class {
    public int $foo = 1;
};

$_ = &$a->foo;

$_ += 1;
var_dump($a->foo);

$_ .= "1";
var_dump($a->foo);

try {
    $_ .= "e50";
} catch (Error $e) { echo $e->getMessage(), "\n"; }
var_dump($a->foo);

$_--;
var_dump($a->foo);

--$_;
var_dump($a->foo);

$a->foo = PHP_INT_MIN;

try {
    $_--;
} catch (Error $e) { echo $e->getMessage(), "\n"; }
echo gettype($a->foo),"\n";

try {
    --$_;
} catch (Error $e) { echo $e->getMessage(), "\n"; }
echo gettype($a->foo),"\n";

$a->foo = PHP_INT_MAX;

try {
    $_++;
} catch (Error $e) { echo $e->getMessage(), "\n"; }
echo gettype($a->foo),"\n";

try {
    ++$_;
} catch (Error $e) { echo $e->getMessage(), "\n"; }
echo gettype($a->foo),"\n";

$_ = 0;
try {
    $_ = [];
} catch (Error $e) { echo $e->getMessage(), "\n"; }
var_dump($a->foo);

$_ = 1;
var_dump($a->foo);

?>