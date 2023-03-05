<?php

${' a'} = ' b';
${' b'} = 'c';
${"b\n b"} = 'b';

var_dump(<<<DOC1
      a
     ${<<<DOC2
        b
        ${<<<DOC3
             a
            DOC3}
        DOC2
     }
    c
    DOC1);

?>