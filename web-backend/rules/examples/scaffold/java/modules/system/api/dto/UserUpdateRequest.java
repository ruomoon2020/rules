package com.company.product.modules.system.api.dto;

public record UserUpdateRequest(
        String email,
        String status
) {
}
