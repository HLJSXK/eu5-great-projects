export function normalizeLocalizationText(value) {
    return value.replace(/\r\n/g, "\n").replace(/\r/g, "\n").replace(/\n/g, " ").trim();
}

export function normalizeMultilineText(value) {
    return value.replace(/\r\n/g, "\n").replace(/\r/g, "\n").trim();
}

const STRUCTURED_FIELD_TYPES = new Set([
    "modifier_table",
    "reward_editor",
    "site_trigger_template",
    "site_preference_template",
]);

export function isStructuredFieldType(fieldType) {
    return STRUCTURED_FIELD_TYPES.has(fieldType);
}

export function stableStringify(value) {
    if (value === null) {
        return "null";
    }
    if (Array.isArray(value)) {
        return `[${value.map((entry) => stableStringify(entry)).join(",")}]`;
    }
    if (typeof value === "object") {
        const keys = Object.keys(value).sort();
        return `{${keys.map((key) => `${JSON.stringify(key)}:${stableStringify(value[key])}`).join(",")}}`;
    }
    return JSON.stringify(value);
}

export function isEditorOptionKey(key) {
    // These names are reserved for UI-only option lists, never source data.
    return key === "options" || key.endsWith("_options");
}

export function withoutEditorOptions(value) {
    if (Array.isArray(value)) {
        return value.map(withoutEditorOptions);
    }
    if (value !== null && typeof value === "object") {
        return Object.fromEntries(Object.entries(value)
            .filter(([key]) => !isEditorOptionKey(key))
            .map(([key, item]) => [key, withoutEditorOptions(item)]));
    }
    return value;
}

export function restoreEditorOptions(draftValue, serverValue) {
    if (Array.isArray(draftValue) && Array.isArray(serverValue)) {
        draftValue.forEach((item, index) => restoreEditorOptions(item, serverValue[index]));
    } else if (draftValue !== null && typeof draftValue === "object" &&
        serverValue !== null && typeof serverValue === "object" && !Array.isArray(serverValue)) {
        for (const [key, item] of Object.entries(serverValue)) {
            if (isEditorOptionKey(key)) {
                draftValue[key] = item;
            } else if (Object.hasOwn(draftValue, key)) {
                restoreEditorOptions(draftValue[key], item);
            }
        }
    }
    return draftValue;
}

export function deepClone(value) {
    return value == null ? value : JSON.parse(JSON.stringify(value));
}

export function parseNumberMaybe(value) {
    const text = String(value ?? "").trim();
    if (!text) {
        return "";
    }
    if (text.toLowerCase() === "yes") return true;
    if (text.toLowerCase() === "no") return false;
    const numeric = text.replace(/(?<=\d)_(?=\d)/g, "");
    if (/^[+-]?\d+$/.test(numeric)) {
        return Number.parseInt(numeric, 10);
    }
    if (/^[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?$/.test(numeric)) {
        return Number.parseFloat(numeric);
    }
    return text;
}

export function rowsToModifierMapping(rows, keyField = "modifier") {
    const mapping = {};
    for (const row of rows || []) {
        const key = String(row?.[keyField] ?? "").trim();
        const value = String(row?.value ?? "").trim();
        if (!key || !value) {
            continue;
        }
        mapping[key] = parseNumberMaybe(value);
    }
    return mapping;
}

export function rowsToStringList(rows) {
    const values = [];
    for (const row of rows || []) {
        const value = String(row?.value ?? "").trim();
        if (!value) {
            continue;
        }
        values.push(value);
    }
    return values;
}

export function rowsToRewardList(rows) {
    const reward = [];
    for (const row of rows || []) {
        const type = String(row?.type ?? "").trim();
        const value = String(row?.value ?? "").trim();
        if (!type || !value) {
            continue;
        }
        reward.push({
            type,
            value: parseNumberMaybe(value),
        });
    }
    return reward;
}

export function asOptionalText(value) {
    const text = normalizeMultilineText(String(value ?? ""));
    return text || null;
}

export function optionByValue(options) {
    const mapping = new Map();
    for (const option of options || []) {
        mapping.set(option.value, option);
    }
    return mapping;
}

export function renderSiteTriggerScript(stateValue) {
    if (stateValue.template_id === "custom_script") {
        return normalizeMultilineText(String(stateValue.raw_script ?? ""));
    }
    const conditionMap = optionByValue(stateValue.condition_options);
    const anyRows = rowsToStringList(stateValue.any_of?.rows);
    const allRows = rowsToStringList(stateValue.all_of?.rows);
    const lines = [];

    if (anyRows.length === 1) {
        lines.push(conditionMap.get(anyRows[0])?.script || anyRows[0]);
    } else if (anyRows.length > 1) {
        lines.push("OR = {");
        for (const value of anyRows) {
            lines.push(`\t${conditionMap.get(value)?.script || value}`);
        }
        lines.push("}");
    }

    for (const value of allRows) {
        lines.push(conditionMap.get(value)?.script || value);
    }

    if (!lines.length) {
        return "always = yes";
    }
    return lines.join("\n");
}

export function renderSitePreferenceScript(stateValue) {
    if (stateValue.template_id === "custom_script") {
        return normalizeMultilineText(String(stateValue.raw_script ?? ""));
    }
    const conditionMap = optionByValue(stateValue.condition_options);
    const sourceMap = optionByValue(stateValue.scale_source_options);
    const lines = [];

    for (const row of stateValue.bonus_rules?.rows || []) {
        const branch = String(row.branch ?? "if").trim() || "if";
        const condition = String(row.condition ?? "").trim();
        const value = String(row.value ?? "").trim();
        if (!condition || !value) {
            continue;
        }
        const script = conditionMap.get(condition)?.script || condition;
        lines.push(`${branch} = {`);
        lines.push(`\tlimit = { var:tv_wonder_survey_site ?= { ${script} } }`);
        lines.push(`\ttv_wonder_change_all_survey_competence_target_effect = { value = ${value} }`);
        lines.push("}");
    }

    let renderedScaled = false;
    for (const row of stateValue.scaled_rules?.rows || []) {
        const source = String(row.source ?? "").trim();
        const min = String(row.min ?? "").trim();
        const max = String(row.max ?? "").trim();
        const multiplier = String(row.multiplier ?? "").trim();
        if (!source || !min || !max || !multiplier) {
            continue;
        }
        const sourcePath = sourceMap.get(source)?.path || source;
        lines.push(`set_variable = { name = tv_wonder_site_preference_bonus value = var:tv_wonder_survey_site.${sourcePath} }`);
        lines.push(`clamp_variable = { name = tv_wonder_site_preference_bonus min = ${min} max = ${max} }`);
        lines.push(`change_variable = { name = tv_wonder_site_preference_bonus multiply = ${multiplier} }`);
        lines.push("tv_wonder_change_all_survey_competence_target_effect = { value = var:tv_wonder_site_preference_bonus }");
        renderedScaled = true;
    }

    if (renderedScaled) {
        lines.push("remove_variable = tv_wonder_site_preference_bonus");
    }

    return lines.join("\n");
}

export function previewPayloadForField(field, stateValue) {
    if (field.field_type === "modifier_table") {
        const mapping = rowsToModifierMapping(stateValue.rows);
        return field.target_kind === "ritual_reward" ? { [field.target_parent_key.split(".")[1]]: mapping } : mapping;
    }
    if (field.field_type === "reward_editor") return { one_shot: rowsToRewardList(stateValue.rows) };
    return stateValue;
}

export function isPlainObject(value) {
    return Boolean(value) && typeof value === "object" && !Array.isArray(value);
}

export function yamlScalar(value) {
    if (value === null) {
        return "null";
    }
    if (typeof value === "number") {
        return String(value);
    }
    if (typeof value === "boolean") {
        return value ? "true" : "false";
    }
    const text = String(value ?? "");
    if (!text) {
        return '""';
    }
    if (/^[A-Za-z_/][A-Za-z0-9_:.+\-/]*$/.test(text) && !/^(?:null|true|false|yes|no|on|off)$/i.test(text)) {
        return text;
    }
    return JSON.stringify(text);
}

export function inlineYamlValue(value) {
    if (Array.isArray(value) && !value.length) {
        return "[]";
    }
    if (isPlainObject(value) && !Object.keys(value).length) {
        return "{}";
    }
    return yamlScalar(value);
}

export function renderYamlLines(value, indent = 0) {
    const prefix = "  ".repeat(indent);
    if (Array.isArray(value)) {
        if (!value.length) {
            return [`${prefix}[]`];
        }
        const lines = [];
        for (const entry of value) {
            if (Array.isArray(entry) || (isPlainObject(entry) && Object.keys(entry).length)) {
                lines.push(`${prefix}-`);
                lines.push(...renderYamlLines(entry, indent + 1));
            } else {
                lines.push(`${prefix}- ${inlineYamlValue(entry)}`);
            }
        }
        return lines;
    }
    if (isPlainObject(value)) {
        const entries = Object.entries(value);
        if (!entries.length) {
            return [`${prefix}{}`];
        }
        const lines = [];
        for (const [key, entry] of entries) {
            if (Array.isArray(entry) || (isPlainObject(entry) && Object.keys(entry).length)) {
                lines.push(`${prefix}${key}:`);
                lines.push(...renderYamlLines(entry, indent + 1));
            } else {
                lines.push(`${prefix}${key}: ${inlineYamlValue(entry)}`);
            }
        }
        return lines;
    }
    return [`${prefix}${inlineYamlValue(value)}`];
}

export function previewTextForField(field, stateValue) {
    if (field.field_type === "site_trigger_template" || field.field_type === "site_preference_template") {
        const script =
            field.field_type === "site_trigger_template"
                ? renderSiteTriggerScript(stateValue)
                : renderSitePreferenceScript(stateValue);
        const lines = [field.target_path || field.key];
        for (const line of String(script || "").split("\n")) {
            lines.push(`  ${line}`);
        }
        return lines.join("\n");
    }
    const payload = previewPayloadForField(field, stateValue);
    const lines = [];
    if (field.target_path) {
        lines.push(`${field.target_path}:`);
        lines.push(...renderYamlLines(payload, 1));
    } else {
        lines.push(...renderYamlLines(payload, 0));
    }
    return lines.join("\n");
}

export function normalizeOption(option) {
    if (typeof option === "string") {
        return {
            value: option,
            label: option,
            key_label: option,
            localized_label: option,
            search_text: option.toLowerCase(),
        };
    }
    const value = String(option?.value ?? "");
    const label = String(option?.label ?? value);
    const keyLabel = String(option?.key_label ?? value);
    const localizedLabel = String(option?.localized_label ?? label);
    const searchText = String(
        option?.search_text ||
            [
                value,
                label,
                keyLabel,
                localizedLabel,
                option?.label_en,
                option?.label_zh,
                option?.description_en,
                option?.description_zh,
                option?.source,
            ]
                .filter(Boolean)
                .join(" "),
    ).toLowerCase();
    return {
        ...option,
        value,
        label,
        key_label: keyLabel,
        localized_label: localizedLabel,
        search_text: searchText,
    };
}

export function normalizeOptionList(options) {
    return (options || []).map(normalizeOption);
}

export function optionsWithBlank(options, blankLabel) {
    const normalized = normalizeOptionList(options);
    if (normalized.some((option) => option.value === "")) {
        return normalized;
    }
    return [
        normalizeOption({
            value: "",
            label: blankLabel,
            key_label: "",
            localized_label: blankLabel,
        }),
        ...normalized,
    ];
}

export function optionPrimaryText(option, displayMode) {
    if (!option) {
        return "";
    }
    return displayMode === "key" ? option.key_label || option.value : option.localized_label || option.label || option.value;
}

export function optionSecondaryText(option, displayMode) {
    if (!option) {
        return "";
    }
    return displayMode === "key" ? option.localized_label || option.label || "" : option.key_label || option.value || "";
}

