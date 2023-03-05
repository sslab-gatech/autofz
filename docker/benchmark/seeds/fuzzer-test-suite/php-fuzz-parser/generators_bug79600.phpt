<?php

function createArrayGenerator() {
    yield from [
        1,
        2,
    ];
}

function createGeneratorFromArrayGenerator() {
    yield from createArrayGenerator();
}

foreach (createGeneratorFromArrayGenerator() as $value) {
    echo $value, "\n";
}

?>