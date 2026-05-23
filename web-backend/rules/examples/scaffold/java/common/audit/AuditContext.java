package com.company.product.common.audit;

import com.company.product.common.observability.TraceIdFilter;
import org.slf4j.MDC;

/**
 * 审计上下文（样板）。业务仓接入 Spring Security 后从 Authentication 解析 operatorId / tenantId / ip。
 */
public final class AuditContext {

    private AuditContext() {}

    public static String currentOperatorId() {
        return "0";
    }

    public static String currentTenantId() {
        return null;
    }

    public static String currentTraceId() {
        return MDC.get(TraceIdFilter.MDC_KEY);
    }
}
