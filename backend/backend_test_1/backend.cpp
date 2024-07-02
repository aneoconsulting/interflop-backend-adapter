

add_float:

    float temp = a + b;
    union {
        float f;
        uint32_t u;
    } converter;
    
    converter.f = temp;
    uint32_t ans = converter.u;

    // ans |= 0x0000000f;
    ans &= 0xfffffff0;
    ans |= 0x00000001;
    
    converter.u = ans;
    *res = converter.f;

end_add_float

add_double:
    *res=a+b;
end_add_double

sub_float:
    *res=a-b;
end_sub_float

sub_double:
    *res=a-b;
end_sub_double

mul_float:
    *res=a*b;
end_mul_float

mul_double:
    *res=a*b;
end_mul_double

div_float:
    *res=a/b;
end_div_float

div_double:
    *res=a/b;
end_div_double

madd_float:
    *res=a*b+c;
end_madd_float

madd_double:
    *res=a*b+c;
end_madd_double

sqrt_float:
    *res=sqrt(a);
end_sqrt_float

sqrt_double:
    *res=sqrt(b);
end_sqrt_double
