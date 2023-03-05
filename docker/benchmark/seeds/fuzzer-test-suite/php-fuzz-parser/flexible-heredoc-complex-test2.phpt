<?php

$a = 'b';
${"b\nb\n d"} = 'b';

var_dump(<<<DOC1
    a
    ${<<<DOC1
        b
        ${<<<DOC1
            a
            DOC1}
         d
        DOC1
    }
    c
    DOC1);

?>