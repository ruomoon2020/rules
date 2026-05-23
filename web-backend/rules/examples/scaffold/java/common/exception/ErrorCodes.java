package com.company.product.common.exception;

/**
 * 业务错误码集中维护（样板）。
 */
public final class ErrorCodes {

    private ErrorCodes() {}

    public static final String USER_NOT_FOUND = "USER_NOT_FOUND";
    public static final String AUDIT_LOG_NOT_FOUND = "AUDIT_LOG_NOT_FOUND";
    public static final String USERNAME_DUPLICATE = "USERNAME_DUPLICATE";
    public static final String CONCURRENT_MODIFICATION = "CONCURRENT_MODIFICATION";
    public static final String INTERNAL_ERROR = "INTERNAL_ERROR";
}
