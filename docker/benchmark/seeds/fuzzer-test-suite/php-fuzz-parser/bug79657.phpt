<?php

function throwException(): iterable
{
    throw new Exception();
}

function loop(): iterable
{
    $callbacks = [
        function () {
            yield 'first';
        },
        function () {
            yield from throwException();
        }
    ];

    foreach ($callbacks as $callback) {
        yield from $callback();
    }
}

function get(string $first, int $second): array
{
    return [];
}

get(...loop());

?>