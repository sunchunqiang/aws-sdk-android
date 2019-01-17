/*
 * Copyright 2010-2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License").
 * You may not use this file except in compliance with the License.
 * A copy of the License is located at
 *
 *  http://aws.amazon.com/apache2.0
 *
 * or in the "license" file accompanying this file. This file is distributed
 * on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
 * express or implied. See the License for the specific language governing
 * permissions and limitations under the License.
 */

package com.amazonaws.services.sqs.model.transform;

import com.amazonaws.Request;
import com.amazonaws.services.sqs.model.*;
import com.amazonaws.util.StringUtils;

/**
 * StAX marshaller for POJO ChangeMessageVisibilityBatchResultEntry
 */
class ChangeMessageVisibilityBatchResultEntryStaxMarshaller {

    public void marshall(
            ChangeMessageVisibilityBatchResultEntry _changeMessageVisibilityBatchResultEntry,
            Request<?> request, String _prefix) {
        String prefix;
        if (_changeMessageVisibilityBatchResultEntry.getId() != null) {
            prefix = _prefix + "Id";
            String id = _changeMessageVisibilityBatchResultEntry.getId();
            request.addParameter(prefix, StringUtils.fromString(id));
        }
    }

    private static ChangeMessageVisibilityBatchResultEntryStaxMarshaller instance;

    public static ChangeMessageVisibilityBatchResultEntryStaxMarshaller getInstance() {
        if (instance == null)
            instance = new ChangeMessageVisibilityBatchResultEntryStaxMarshaller();
        return instance;
    }
}
