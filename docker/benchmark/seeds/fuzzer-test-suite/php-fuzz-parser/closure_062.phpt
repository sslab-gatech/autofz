<?php

class Test {
    public function method() {
        echo "instance scoped, non-static, \$this used\n";
        $fn = function() {
            var_dump($this);
        };
        $fn->bindTo(null);
        echo "instance scoped, static, \$this used\n";
        $fn = static function() {
            var_dump($this);
        };
        $fn->bindTo(null);
        echo "instance scoped, non-static, \$this not used\n";
        $fn = function() {
            var_dump($notThis);
        };
        $fn->bindTo(null);
    }

    public static function staticMethod() {
        echo "static scoped, non-static, \$this used\n";
        $fn = function() {
            var_dump($this);
        };
        $fn->bindTo(null);
        echo "static scoped, static, \$this used\n";
        $fn = static function() {
            var_dump($this);
        };
        $fn->bindTo(null);
        echo "static scoped, static, \$this not used\n";
        $fn = function() {
            var_dump($notThis);
        };
        $fn->bindTo(null);
    }
}

(new Test)->method();
Test::staticMethod();

?>