<?php

$code = <<<'CODE'
function test_missing_semicolon() : string {
     $x = []
     FOO
}
CODE;

try {
    eval($code);
} catch (ParseError $e) {
    var_dump($e->getMessage());
}

try {
    eval($code);
} catch (ParseError $e) {
    var_dump($e->getMessage());
}

?>