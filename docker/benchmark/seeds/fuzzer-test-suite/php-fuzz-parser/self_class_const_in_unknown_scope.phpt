<?php

class Test {
    public function foobar() {
        eval("
            const FOO = self::class;
            var_dump(FOO);
        ");
    }
}
(new Test)->foobar();

const BAR = self::class;
var_dump(BAR);

?>