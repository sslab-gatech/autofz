<?php
declare(strict_types=1);

function foo(): mixed
{
}

try {
    foo();
} catch (TypeError $exception) {
    echo $exception->getMessage() . "\n";
}

?>