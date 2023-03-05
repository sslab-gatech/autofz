<?php

function try_eval($code) {
    try {
        eval($code);
    } catch (CompileError $e) {
        echo $e->getMessage(), "\n";
    }
}

try_eval('if (false) {class C { final final function foo($fff) {}}}');
try_eval('if (false) {class C { private protected $x; }}');
try_eval('if (true) { __HALT_COMPILER(); }');
try_eval('declare(encoding=[]);');

?>