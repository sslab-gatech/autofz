<?php

$a = new class {
    public int $foo = 1;
};

$_ = [&$a->foo];

$_[0] += 1;
var_dump($a->foo);

$_[0] .= "1";
var_dump($a->foo);

try {
    $_[0] .= "e50";
} catch (Error $e) { echo $e->getMessage(), "\n"; }
var_dump($a->foo);

$_[0]--;
var_dump($a->foo);

--$_[0];
var_dump($a->foo);

$a->foo = PHP_INT_MIN;

try {
        $_[0]--;
} catch (Error $e) { echo $e->getMessage(), "\n"; }
echo gettype($a->foo),"\n";

try {
    --$_[0];
} catch (Error $e) { echo $e->getMessage(), "\n"; }
echo gettype($a->foo),"\n";

$a->foo = PHP_INT_MAX;

try {
    $_[0]++;
} catch (Error $e) { echo $e->getMessage(), "\n"; }
echo gettype($a->foo),"\n";

try {
    ++$_[0];
} catch (Error $e) { echo $e->getMessage(), "\n"; }
echo gettype($a->foo),"\n";

$_[0] = 0;
try {
    $_[0] = [];
} catch (Error $e) { echo $e->getMessage(), "\n"; }
var_dump($a->foo);

$_[0] = 1;
var_dump($a->foo);

?>