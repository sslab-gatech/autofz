<?php

function foo(): mixed
{
}

try {
    foo();
} catch (TypeError $exception) {
    echo $exception->getMessage() . "\n";
}

?>