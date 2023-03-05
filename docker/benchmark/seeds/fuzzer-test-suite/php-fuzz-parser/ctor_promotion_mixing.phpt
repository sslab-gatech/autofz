<?php

class Test {
    public string $prop2;

    public function __construct(public string $prop1 = "", $param2 = "") {
        $this->prop2 = $prop1 . $param2;
    }
}

var_dump(new Test("Foo", "Bar"));
echo "\n";
echo new ReflectionClass(Test::class), "\n";

?>