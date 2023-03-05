<?php

<<Attribute(Attribute::TARGET_FUNCTION)>>
class A1
{
	public string $name;
	public int $ttl;

	public function __construct(string $name, int $ttl = 50)
	{
		$this->name = $name;
		$this->ttl = $ttl;
	}
}

$ref = new \ReflectionFunction(<<A1('test')>> function () { });

foreach ($ref->getAttributes() as $attr) {
	$obj = $attr->newInstance();

	var_dump(get_class($obj), $obj->name, $obj->ttl);
}

echo "\n";

$ref = new \ReflectionFunction(<<A1>> function () { });

try {
	$ref->getAttributes()[0]->newInstance();
} catch (\ArgumentCountError $e) {
	var_dump('ERROR 1', $e->getMessage());
}

echo "\n";

$ref = new \ReflectionFunction(<<A1([])>> function () { });

try {
	$ref->getAttributes()[0]->newInstance();
} catch (\TypeError $e) {
	var_dump('ERROR 2', $e->getMessage());
}

echo "\n";

$ref = new \ReflectionFunction(<<A2>> function () { });

try {
	$ref->getAttributes()[0]->newInstance();
} catch (\Error $e) {
	var_dump('ERROR 3', $e->getMessage());
}

echo "\n";

<<Attribute>>
class A3
{
	private function __construct() { }
}

$ref = new \ReflectionFunction(<<A3>> function () { });

try {
	$ref->getAttributes()[0]->newInstance();
} catch (\Error $e) {
	var_dump('ERROR 4', $e->getMessage());
}

echo "\n";

<<Attribute>>
class A4 { }

$ref = new \ReflectionFunction(<<A4(1)>> function () { });

try {
	$ref->getAttributes()[0]->newInstance();
} catch (\Error $e) {
	var_dump('ERROR 5', $e->getMessage());
}

echo "\n";

class A5 { }

$ref = new \ReflectionFunction(<<A5>> function () { });

try {
	$ref->getAttributes()[0]->newInstance();
} catch (\Error $e) {
	var_dump('ERROR 6', $e->getMessage());
}

?>