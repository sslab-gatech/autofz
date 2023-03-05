<?php

trait SomeTrait {
    public function foobar() {}
}

class Test {
    use SomeTrait {
        SomeTrait::foobar insteadof static;
    }
}

?>