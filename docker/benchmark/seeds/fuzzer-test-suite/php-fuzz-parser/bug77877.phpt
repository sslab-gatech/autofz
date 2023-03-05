<?php
class Foo {
    static public function bar() {
        var_dump($this);
    }
}
try {
    array_map([new Foo, 'bar'],[1]);
} catch (Throwable $e) {
    echo $e->getMessage() . "\n";
}
try {
    call_user_func([new Foo, 'bar']);
} catch (Throwable $e) {
    echo $e->getMessage() . "\n";
}
?>