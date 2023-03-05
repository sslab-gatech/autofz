<?php

final class Test {
    public static function create(): static {
        return new static;
    }
}

var_dump(Test::create());

?>