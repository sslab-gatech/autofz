<?php

trait SomeTrait {
    public function foobar() {}
}

class Test {
    use SomeTrait {
        static::foobar insteadof SomeTrait;
    }
}

?>