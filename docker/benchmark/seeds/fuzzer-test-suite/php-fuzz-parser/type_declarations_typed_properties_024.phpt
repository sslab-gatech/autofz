<?php
class Foo {
    private int $thing;
}

class Bar extends Foo {
    public string $thing; // No conflict
}

echo "ok";
?>