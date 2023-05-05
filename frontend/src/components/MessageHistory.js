import React from 'react';

const MessageHistory = ({ messageHistory }) => {
    return (
        <div className="message-history">
            <h2>Message History</h2>
            <ul>
                {messageHistory.map((message, index) => (
                    <li key={index}>
                        <div>
                            <strong>Script:</strong> {message.refine}
                        </div>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default MessageHistory;
