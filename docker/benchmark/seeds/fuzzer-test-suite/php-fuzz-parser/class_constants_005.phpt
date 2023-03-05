<?php
define ("A", "." . ord(26) . ".");
eval("class A {const a = A;}");
var_dump(A::a);
?>