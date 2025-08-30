def divide_ceil(n):
    # 计算商和余数
    quotient = n // 10
    remainder = n % 10
    # 如果有余数则商加1
    if remainder > 0:
        quotient += 1
    return quotient