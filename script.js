import { initializeApp } from "https://www.gstatic.com/firebasejs/11.6.1/firebase-app.js";
import { getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword, signOut, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/11.6.1/firebase-auth.js";

const firebaseConfig = {
  apiKey: "AIzaSyB57grLakj5bWSNadzCHNm4EwjiUshOycg",
  authDomain: "finance-9d19f.firebaseapp.com",
  projectId: "finance-9d19f",
  storageBucket: "finance-9d19f.appspot.com",
  messagingSenderId: "155107732176",
  appId: "1:155107732176:web:517132b58d187e25218cd5",
  measurementId: "G-GRFKH8LNRB"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth();

const authSection = document.getElementById('auth-section');
const appSection = document.getElementById('app-section');

onAuthStateChanged(auth, user => {
  if (user) {
    authSection.style.display = 'none';
    appSection.style.display = 'block';
  } else {
    authSection.style.display = 'block';
    appSection.style.display = 'none';
  }
});

window.register = () => {
  const email = document.getElementById('reg-email').value;
  const password = document.getElementById('reg-password').value;
  createUserWithEmailAndPassword(auth, email, password)
    .then(() => alert('Registered successfully!'))
    .catch(err => alert(err.message));
};

window.login = () => {
  const email = document.getElementById('login-email').value;
  const password = document.getElementById('login-password').value;
  signInWithEmailAndPassword(auth, email, password)
    .catch(err => alert(err.message));
};

window.logout = () => {
  signOut(auth);
};

window.toggleDarkMode = () => {
  document.body.classList.toggle('dark');
};

const form = document.getElementById('transaction-form');
const transactionsTableBody = document.getElementById('transactions-body');
const totalIncome = document.getElementById('total-income');
const totalExpense = document.getElementById('total-expense');
const balance = document.getElementById('balance');

let transactions = [];

form.addEventListener('submit', e => {
  e.preventDefault();
  const desc = document.getElementById('desc').value;
  const amount = parseFloat(document.getElementById('amount').value);
  const type = document.getElementById('type').value;
  const currency = document.getElementById('currency').value;
  const category = document.getElementById('category').value;

  if (!desc || isNaN(amount)) return;

  const transaction = {
    id: Date.now(),
    desc,
    amount,
    type,
    currency,
    category
  };

  transactions.push(transaction);
  form.reset();
  renderTransactions();
  updateSummary();
});

function renderTransactions() {
  transactionsTableBody.innerHTML = '';
  transactions.forEach(tx => {
    const row = document.createElement('tr');
    row.classList.add(tx.type);

    row.innerHTML = `
      <td>${tx.desc}</td>
      <td>${tx.category}</td>
      <td>${tx.type}</td>
      <td>${tx.currency}${tx.amount.toFixed(2)}</td>
    `;

    transactionsTableBody.appendChild(row);
  });
}

function updateSummary() {
  let income = 0, expense = 0;
  transactions.forEach(t => {
    if (t.type === 'income') income += t.amount;
    else expense += t.amount;
  });

  const curr = transactions[0]?.currency || '₹';
  totalIncome.textContent = curr + income.toFixed(2);
  totalExpense.textContent = curr + expense.toFixed(2);
  balance.textContent = curr + (income - expense).toFixed(2);
}
