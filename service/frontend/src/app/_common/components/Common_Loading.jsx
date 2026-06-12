import React from "react";
import { SyncLoader } from "react-spinners";

const Loading = () => {
    return (
        <div>
            <h2 className="common__loading__text">Waiting</h2>
            <SyncLoader />
        </div>
    );
};

export default Loading