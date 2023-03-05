<?php

interface I {
    public function test(): Generator|ArrayAccess|array;
}
class C implements I {
    function test(): Generator|ArrayAccess|array {
        yield;
    }
}

?>
===DONE===