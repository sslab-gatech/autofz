<?php

class A  {
    const B = 1;
}
try {
    constant('A::B1');
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}

?>