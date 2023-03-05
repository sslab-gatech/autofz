<?php

function test($x) {
}
test(new class {
    public function __destruct() {
        debug_print_backtrace();
    }
});

?>