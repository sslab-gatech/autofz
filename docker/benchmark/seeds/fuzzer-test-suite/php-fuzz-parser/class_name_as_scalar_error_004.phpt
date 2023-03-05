<?php

namespace Foo\Bar {
    class One {}
    class Two extends One {
        public function baz($x = parent::class) {
            var_dump($x);
        }
    }
    (new Two)->baz();
}
?>