<?php
declare(strict_types=1);
try {
    substr("foo");
} catch (ArgumentCountError $e) {
    echo get_class($e) . PHP_EOL;
    echo $e->getMessage() . PHP_EOL;
}

try {
    array_diff([]);
} catch (ArgumentCountError $e) {
    echo get_class($e) . PHP_EOL;
    echo $e->getMessage(), "\n";
}