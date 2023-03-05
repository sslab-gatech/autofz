<?php

$ref = new \ReflectionFunction(<<A1>> <<A2>> function () { });
$attr = $ref->getAttributes(A3::class);

var_dump(count($attr));

$ref = new \ReflectionFunction(<<A1>> <<A2>> function () { });
$attr = $ref->getAttributes(A2::class);

var_dump(count($attr), $attr[0]->getName());

$ref = new \ReflectionFunction(<<A1>> <<A2>> <<A2>> function () { });
$attr = $ref->getAttributes(A2::class);

var_dump(count($attr), $attr[0]->getName(), $attr[1]->getName());

echo "\n";

interface Base { }
class A1 implements Base { }
class A2 implements Base { }
class A3 extends A2 { }

$ref = new \ReflectionFunction(<<A1>> <<A2>> <<A5>> function () { });
$attr = $ref->getAttributes(\stdClass::class, \ReflectionAttribute::IS_INSTANCEOF);
var_dump(count($attr));
print_r(array_map(fn ($a) => $a->getName(), $attr));

$ref = new \ReflectionFunction(<<A1>> <<A2>> function () { });
$attr = $ref->getAttributes(A1::class, \ReflectionAttribute::IS_INSTANCEOF);
var_dump(count($attr));
print_r(array_map(fn ($a) => $a->getName(), $attr));

$ref = new \ReflectionFunction(<<A1>> <<A2>> function () { });
$attr = $ref->getAttributes(Base::class, \ReflectionAttribute::IS_INSTANCEOF);
var_dump(count($attr));
print_r(array_map(fn ($a) => $a->getName(), $attr));

$ref = new \ReflectionFunction(<<A1>> <<A2>> <<A3>> function () { });
$attr = $ref->getAttributes(A2::class, \ReflectionAttribute::IS_INSTANCEOF);
var_dump(count($attr));
print_r(array_map(fn ($a) => $a->getName(), $attr));

$ref = new \ReflectionFunction(<<A1>> <<A2>> <<A3>> function () { });
$attr = $ref->getAttributes(Base::class, \ReflectionAttribute::IS_INSTANCEOF);
var_dump(count($attr));
print_r(array_map(fn ($a) => $a->getName(), $attr));

echo "\n";

$ref = new \ReflectionFunction(function () { });

try {
	$ref->getAttributes(A1::class, 3);
} catch (\Error $e) {
	var_dump('ERROR 1', $e->getMessage());
}

$ref = new \ReflectionFunction(function () { });

try {
	$ref->getAttributes(SomeMissingClass::class, \ReflectionAttribute::IS_INSTANCEOF);
} catch (\Error $e) {
	var_dump('ERROR 2', $e->getMessage());
}

?>