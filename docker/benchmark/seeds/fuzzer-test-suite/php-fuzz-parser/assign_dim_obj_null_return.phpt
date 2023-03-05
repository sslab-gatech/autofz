<?php

function test() {
    $array = [PHP_INT_MAX => 42];
    $true = true;

    try {
        var_dump($array[] = 123);
    } catch (Error $e) {
        echo $e->getMessage(), "\n";
    }

    try {
        var_dump($array[[]] = 123);
    } catch (Error $e) {
        echo $e->getMessage(), "\n";
    }

    try {
        var_dump($array[new stdClass] = 123);
    } catch (Error $e) {
        echo $e->getMessage(), "\n";
    }

    try {
        var_dump($true[123] = 456);
    } catch (Error $e) {
        echo $e->getMessage(), "\n";
    }

    try {
        var_dump($array[] += 123);
    } catch (Error $e) {
        echo $e->getMessage(), "\n";
    }

    try {
        var_dump($array[[]] += 123);
    } catch (Error $e) {
        echo $e->getMessage(), "\n";
    }

    try {
        var_dump($array[new stdClass] += 123);
    } catch (Error $e) {
        echo $e->getMessage(), "\n";
    }

    try {
        var_dump($true[123] += 456);
    } catch (Error $e) {
        echo $e->getMessage(), "\n";
    }

    try {
        var_dump($true->foo = 123);
    } catch (Error $e) {
        echo $e->getMessage(), "\n";
    }
    try {
        var_dump($true->foo += 123);
    } catch (Error $e) {
        echo $e->getMessage(), "\n";
    }
}

test();

?>