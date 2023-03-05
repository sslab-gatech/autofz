<?php

class Test {
    private $prop = "Test";

    function run() {
        foreach ($this as $k => $v) {
            echo "$k => $v\n";
        }
        var_dump(get_object_vars($this));
    }
}
class Test2 extends Test {
    public $prop = "Test2";
}

(new Test2)->run();

?>