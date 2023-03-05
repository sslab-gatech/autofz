<?php
$array = [1, 2, 3];

function getArr() {
    return [4, 5];
}

function arrGen() {
    for($i = 11; $i < 15; $i++) {
        yield $i;
    }
}

var_dump([...[]]);
var_dump([...[1, 2, 3]]);
var_dump([...$array]);
var_dump([...getArr()]);
var_dump([...arrGen()]);
var_dump([...new ArrayIterator(['a', 'b', 'c'])]);

var_dump([0, ...$array, ...getArr(), 6, 7, 8, 9, 10, ...arrGen()]);
var_dump([0, ...$array, ...$array, 'end']);
