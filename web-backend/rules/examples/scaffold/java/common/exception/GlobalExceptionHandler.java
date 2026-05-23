package com.company.product.common.exception;

import com.company.product.common.web.ApiResult;
import jakarta.servlet.http.HttpServletRequest;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.slf4j.MDC;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

/**
 * 全局异常处理（样板）。日志勿输出敏感参数。
 */
@RestControllerAdvice
public class GlobalExceptionHandler {

    private static final Logger log = LoggerFactory.getLogger(GlobalExceptionHandler.class);

    @ExceptionHandler(BusinessException.class)
    public ResponseEntity<ApiResult<Void>> handleBusiness(BusinessException ex, HttpServletRequest request) {
        String traceId = MDC.get("traceId");
        return ResponseEntity
                .status(ex.getHttpStatus())
                .body(ApiResult.fail(ex.getHttpStatus().value(), ex.getMessage(), ex.getErrorCode(), traceId));
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<ApiResult<Void>> handleUnknown(Exception ex) {
        String traceId = MDC.get("traceId");
        log.error("event=system.unhandled.failed traceId={}", traceId, ex);
        return ResponseEntity
                .status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body(ApiResult.fail(500, "系统繁忙", ErrorCodes.INTERNAL_ERROR, traceId));
    }
}
