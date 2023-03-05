<?php

$a = new class {
    public ?iterable $it = [];
    public ?array $a;
    public ?Traversable $t;
};

$ref = &$a->it;
$a->a = &$ref;

var_dump($ref);

try {
    $a->t = &$ref;
} catch (TypeError $e) { var_dump($e->getMessage()); }
var_dump($ref);

$a->it = [1]; // type is still assignable
var_dump($ref);

try {
    $ref = new ArrayIterator();
} catch (TypeError $e) { var_dump($e->getMessage()); }
var_dump($ref instanceof ArrayIterator);

unset($a->a);

$ref = null;

$a->t = &$ref;

try {
    $ref = [];
} catch (TypeError $e) { var_dump($e->getMessage()); }
var_dump($ref instanceof ArrayIterator);

$ref = new ArrayIterator();
var_dump($ref instanceof ArrayIterator);

?>