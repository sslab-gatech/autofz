<?php
trait PropertiesTrait
{
    public $same = true;
}

class PropertiesExample
{
    use PropertiesTrait;
    public $same = 2;
}
?>