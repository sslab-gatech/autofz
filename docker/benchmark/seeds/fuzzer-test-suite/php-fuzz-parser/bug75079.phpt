<?php

trait Foo
{
    public function selfDo(self ...$Selfs)
    {
        array_map(
            function (self $Self) : self
            {
                return $Self;
            },
            $Selfs
        );
    }
}

class Bar
{
    use Foo;
}

class Baz
{
    use Foo;
}

$Bar = new Bar;
$Baz = new Baz;

$Bar->selfDo($Bar, $Bar);
$Baz->selfDo($Baz, $Baz);

?>
===DONE===