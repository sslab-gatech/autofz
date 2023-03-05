<?php
$foo = new class {
    public ?int $bar;
};

$bar = &$foo->bar;

$bar *= 1;

var_dump($bar--);
var_dump(--$bar);
var_dump(++$bar);
var_dump($bar++);

$bar = PHP_INT_MAX;

try {
    var_dump($bar++);
} catch (Throwable $e) {
    echo $e->getMessage() . "\n";
}

try {
    var_dump(++$bar);
} catch (Throwable $e) {
    echo $e->getMessage() . "\n";
}

$bar = PHP_INT_MIN;


try {
    var_dump($bar--);
} catch (Throwable $e) {
    echo $e->getMessage() . "\n";
}

try {
    var_dump(--$bar);
} catch (Throwable $e) {
    echo $e->getMessage() . "\n";
}

?>